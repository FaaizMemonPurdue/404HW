from gen_key_schedule import round_key_driver
from gen_tables import genTables
import sys as sys

inputFile = open(sys.argv[2]) #input text (cipher or plain)
inputText = inputFile.read()
inputFile.close()

keyFile = open(sys.argv[3])
keyText = keyFile.read()
keyFile.close()
round_keys = round_key_driver(keyText)