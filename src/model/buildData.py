import re
import collections
import random
import json
import sys
import os
import os.path

PAD = 1
UNK = 2
START = 3
END = 4

def tokenizeNL(nl):
  nl = nl.strip().decode('utf-8').encode('ascii', 'replace')
  return nl.split() # tokenization is done before codenn (funcom project)
  # return re.findall(r"[\w]+|[^\s\w]", nl)

def tokenizeCode(code, parsefunc):
  code = code.strip().decode('utf-8').encode('ascii', 'replace')
  typedCode = parsefunc(code)
  tokens = [re.sub( '\s+', ' ', x.strip())  for x in typedCode]
  return tokens

# lang can be csharp or code
def buildVocab(filename, code_unk_threshold, nl_unk_threshold, lang, parsefunc):
  vocabfile = os.environ["CODENN_WORK"] + '/vocab.' + lang
  if os.path.isfile(vocabfile):
    with open(vocabfile) as json_vocabfile:
      return json.load(json_vocabfile)

    
  vocab = {
    "nl_to_num": {"UNK": UNK, "CODE_START": START, "CODE_END": END},
    "code_to_num": {"UNK": UNK, "CODE_START": START, "CODE_END": END},
    "num_to_nl": {PAD: "UNK", UNK: "UNK", START: "CODE_START", END: "CODE_END"},
    "num_to_code": {UNK: "UNK", START: "CODE_START", END: "CODE_END"},
  }

  words = collections.Counter()
  tokens = collections.Counter()

  for line in open(filename, "r"):
    qid, rid, nl, code, weight = line.strip().split('\t')
    tokens.update(tokenizeCode(code, parsefunc))
    words.update(tokenizeNL(nl))

  token_count = END + 1
  nl_count = END + 1

  # Do unigram tokens
  for tok in tokens:
    if tokens[tok] > code_unk_threshold:
      vocab["code_to_num"][tok] = token_count
      vocab["num_to_code"][token_count] = tok
      token_count += 1
    else:
      vocab["code_to_num"][tok] = UNK

  for word in words:
    if words[word] > nl_unk_threshold:
      vocab["nl_to_num"][word] = nl_count
      vocab["num_to_nl"][nl_count] = word
      nl_count += 1
    else:
      vocab["nl_to_num"][word] = UNK

  vocab["max_code"] = token_count - 1
  vocab["max_nl"] = nl_count - 1
  vocab["lang"] = lang

  f = open(os.environ["CODENN_WORK"] + '/vocab.' + lang, 'w')
  f.write(json.dumps(vocab))
  f.close()

  return vocab


def get_data(filename, vocab, dont_skip, max_code_length, max_nl_length, parsefunc):
  lang = vocab["lang"]
  dataset = []
  skipped = 0
  for line in open(filename, 'r'):

    qid, rid, nl, code, wt = line.strip().split('\t')
    codeToks  = tokenizeCode(code, parsefunc)
    nlToks = tokenizeNL(nl)

    datasetEntry = {"id": rid, "code": code, "code_sizes": len(codeToks), "code_num":[], "nl":[], "nl_num":[]}

    for tok in codeToks:
      if tok not in vocab["code_to_num"]:
        vocab["code_to_num"][tok] = UNK
      datasetEntry["code_num"].append(vocab["code_to_num"][tok])

    datasetEntry["nl_num"].append(vocab["nl_to_num"]["CODE_START"])
    for word in nlToks:
      if word not in vocab["nl_to_num"]:
        vocab["nl_to_num"][word] = UNK
      datasetEntry["nl_num"].append(vocab["nl_to_num"][word])
      datasetEntry["nl"].append(word)

    datasetEntry["nl_num"].append(vocab["nl_to_num"]["CODE_END"])

    if dont_skip or (len(datasetEntry["code_num"]) <= max_code_length and len(datasetEntry["nl_num"]) <= max_nl_length):
      dataset.append(datasetEntry)
    else:
      skipped += 1

  print 'Total size = ' + str(len(dataset))
  print 'Total skipped = ' + str(skipped)

  f = open(os.environ["CODENN_WORK"] + '/' + os.path.basename(filename) + "." + lang, 'w')
  f.write(json.dumps(dataset))
  f.close()

  f3 = open(os.environ["CODENN_WORK"] + '/' + os.path.basename(filename) + "." + lang + ".ref", 'w')
  f4 = open(os.environ["CODENN_WORK"] + '/' + os.path.basename(filename) + "." + lang + ".ref.final", 'w')
  for entry in dataset:
    f3.write(entry["id"] + '\t' + ' '.join(entry["nl"]) + '\n')
    f4.write(' '.join(entry["nl"]) + '\n')
    
  f3.close()
  f4.close()


def checkfile(fname):
  if os.path.isfile(fname):
    return
  else:
    print 'file ' + fname + ' does not exist.'
    sys.exit(1)

    
if __name__ == '__main__':

  lang = sys.argv[1]
  max_code_len = int(sys.argv[2])
  max_nl_len = int(sys.argv[3])
  code_unk_threshold = int(sys.argv[4])
  nl_unk_threshold = int(sys.argv[5])

  datadir = os.path.join(os.environ['CODENN_DIR'], 'data/', lang)
  parsefunc = None
  if lang == 'cpp':
    from cpp.CppTemplate import parseCpp
    parsefunc = parseCpp    
  elif lang == 'java':
    from java.JavaTemplate import parseJava
    parsefunc = parseJava
  else:
    print 'lang should be cpp or java instead of ' + lang
    sys.exit(1)

  trainfile=os.path.join(datadir, 'train.txt')
  validfile=os.path.join(datadir, 'valid.txt')
  testfile =os.path.join(datadir, 'test.txt' )
  
  checkfile(trainfile)
  checkfile(validfile)
  checkfile(testfile)
  
  vocab = buildVocab(trainfile, code_unk_threshold, nl_unk_threshold, lang, parsefunc)
  get_data(trainfile, vocab, False, max_code_len, max_nl_len, parsefunc)
  get_data(validfile, vocab, False, max_code_len, max_nl_len, parsefunc)
  get_data(testfile, vocab, False, max_code_len, max_nl_len, parsefunc)
