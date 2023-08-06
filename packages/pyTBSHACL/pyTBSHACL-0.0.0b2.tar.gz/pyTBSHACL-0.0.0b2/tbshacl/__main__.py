"""

"""
import os
import sys
import argparse
import logging
import tbshacl
import tempfile
import rdflib

def reportTextFromGraph(result_ttl):
    """
    Hack for getting conformance boolean.

    TODO: process the result graph to generate some human output.
    """
    rg = rdflib.Graph()
    rg.parse(data=result_ttl, format="turtle")
    CF = rdflib.URIRef("http://www.w3.org/ns/shacl#conforms")
    conforms = False
    for subject, predicate, obj in rg:
        #print(f"{subject}  {predicate}  {obj}")
        if predicate == CF:
            conforms = (obj.lower() in ['true', ])
    res = "CONFORMS = " + str(conforms)
    return res


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-l', '--log_level',
                        action='count',
                        default=0,
                        help='Set logging level, multiples for more detailed.')
    parser.add_argument("-d","--datafile",
                        default=None,
                        help="Path to data file in turtle format")
    parser.add_argument("-df", "--data_format", default="turtle",
                        help="Format of data_file (turtle)")
    parser.add_argument("-s","--shapefile",
                        default=None,
                        help="Optional path to shape file in turtle format")
    args = parser.parse_args()
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(len(levels) - 1, args.log_level)]
    logging.basicConfig(level=level,
                        format="%(asctime)s %(levelname)s %(message)s")
    if args.datafile is None:
        logging.error("Datafile is required.")
        return 1
    data_file = args.datafile
    temp_name = None
    if args.data_format.lower() != "turtle":
        # Create a temporary file to hold the converted RDF
        fdest, temp_name = tempfile.mkstemp(suffix=".ttl")
        os.close(fdest)
        g = rdflib.Graph()
        g.parse(source=args.datafile, format=args.data_format)
        g.serialize(temp_name, format="turtle")
        data_file = temp_name
        logging.debug("Wrote turtle to " + data_file)
        with open(data_file, "r") as ftmp:
            logging.debug(ftmp.read())
    resout, reserr = tbshacl.tbShaclValidate(data_file, shape_file=args.shapefile)
    if not temp_name is None:
        os.unlink(temp_name)
    if resout is None:
        return 2
    sys.stderr.write(reserr.decode())
    sys.stdout.write(resout.decode())
    print("===")
    print(reportTextFromGraph(resout))
    return 0

if __name__ == "__main__":
    sys.exit(main())