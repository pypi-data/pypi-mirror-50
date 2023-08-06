import logging
import subprocess
import os


def tbShaclValidate(data_file, shape_file=None):
    try:
        shacl_validate = os.path.join(os.environ["SHACLROOT"], "shaclvalidate.sh")
    except KeyError as e:
        logging.error("Environment variable SHACLROOT must point to the folder containing shaclvalidate.sh")
        return None,None
    args = [shacl_validate, "-datafile", data_file]
    if shape_file is not None:
        args.append("-shapesfile")
        args.append(shape_file)
    completed = subprocess.run(args,capture_output=True)
    logging.debug("ARGS=" + str(completed.args))
    return completed.stdout, completed.stderr

