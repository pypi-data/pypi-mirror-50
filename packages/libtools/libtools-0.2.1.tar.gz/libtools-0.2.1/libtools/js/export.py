import sys
import json
import inspect
from pygments import highlight, lexers, formatters
from libtools import logger


def export_iterobject(dict_obj, filename=None, logging=True):
    """
    Summary:
        pretty prints json, list, and tuple objects or exports iter
        object schema to filesystem object on the local filesystem

    Args:
        :dict_obj (dict): dictionary object
        :filename (str):  name of file to be exported (optional)

    Returns:
        True | False Boolean export status

    """
    def is_tty():
        """
        Summary:
            Determines if output is displayed to the screen or redirected
        Returns:
            True if tty terminal | False is redirected, TYPE: bool
        """
        return sys.stdout.isatty()

    try:

        if filename:

            try:

                with open(filename, 'w') as handle:
                    handle.write(json.dumps(dict_obj, indent=4, sort_keys=True))
                    logger.info(
                        '%s: Wrote %s to local filesystem location' %
                        (inspect.stack()[0][3], filename))
                handle.close()

            except TypeError as e:
                fx = inspect.stack()[0][3]
                logger.warning('{}: object in dict not serializable: {}'.format(fx, str(e)))
                raise e

        elif is_tty():
            try:

                # convert dict schema to json
                json_str = json.dumps(dict_obj, indent=4, sort_keys=True)

                print(
                    highlight(
                        json_str,
                        lexers.JsonLexer(),
                        formatters.TerminalFormatter()
                    ).strip()
                )
            except TypeError as e:
                logger.info('element in json not serializable ({})'.format(e))
            if logging:
                logger.info('{}: successful export to stdout'.format(inspect.stack()[0][3]))
            return True

        else:
            # print output, but not to stdout; possibly commandline redirect
            print(json.dumps(dict_obj, indent=4, sort_keys=True))

    except OSError as e:
        logger.critical(
            '%s: export_file_object: error writing to %s to filesystem. Error: %s' %
            (inspect.stack()[0][3], filename, str(e)))
        return False
    if logging:
        logger.info('export_file_object: successful export to {}'.format(filename))
    return True
