from astinxml.Documenter import Documenter
import sys

print(Documenter().parse_module(sys.argv[1]).toprettyxml()) # pragma: no mutate
 
