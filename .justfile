help:
  python src/main.py --help

test: test-json

test-json:
  python src/main.py test/PG2L100H_FBG676.bsm --output test/output.json --format json
  
test-get-port:
  python src/main.py test/PG2L100H_FBG676.bsm --output test/output.json --method GetLogicPortDesp

test-get-boundary-reg:
  python src/main.py test/PG2L100H_FBG676.bsm --output test/output.json --method GetBoundaryScanRegDesp