import sys
import classmodule
import funcmodule

if len(sys.argv()) < 2:
    print("Please provide a path towards the instructions file")
    sys.exit()

with open(sys.argv[1], 'r') as stream:
    parsed = funcmodule.parse_config(stream)

try:
    commands = parsed["commands"]
    expect = parsed["expect"]

except KeyError:
    print("Missing element in the dictionary.")
    sys.exit()

command = classmodule.Commands(commands, expect)

command.run()
