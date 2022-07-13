from flask import Response
    
def magic_link_error(message):
    return Response (
        "Incorrect MAGIC LINK data, please check the contents of"
        " the MAGIC LINK data. Example data:"
        f" {message}"
    ), 400
            
def application_submission_error(message):
    return Response (
        "Incorrect APPLICATION data, please check the contents of"
        " the APPLICATION data. \nExample data:"
        f" {message}"
    ), 400


def template_type_error(message):
    return Response (
        f"Incorrect type, please check the value of key 'type': {message.get('type')}. Expected"
        " type:('MAGIC_LINK' or 'NOTIFICATION' or 'REMINDER' or"
        f" 'AWARD' or 'APPLICATION_RECORD_OF_SUBMISSION')." 
    ), 400
         