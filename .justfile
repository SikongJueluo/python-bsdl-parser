help:
  python src/main.py --help

test: test-json
  
build-release: 
  python -m nuitka --mode=standalone src/main.py
  cp -r src/bsdl.lark main.dist/bsdl.lark
  
build-single: 
  python -m nuitka --onefile --include-data-file=./src/bsdl.lark=./ --output-dir=dist ./src/main.py

test-json:
  python src/main.py test/PG2L100H_FBG676.bsm --output test/output.json --format json
  
test-get-port:
  python src/main.py test/PG2L100H_FBG676.bsm --output test/output.json --method GetLogicPortDesp

test-get-boundary-reg:
  python src/main.py test/PG2L100H_FBG676.bsm --output test/output.json --method GetBoundaryScanRegDesp

test-print-port:
  python src/main.py test/PG2L100H_FBG676.bsm --output test/output.json --format str --method GetLogicPortDesp

test-print-boundary-reg:
  python src/main.py test/PG2L100H_FBG676.bsm --output test/output.json --format str --method GetBoundaryScanRegDesp