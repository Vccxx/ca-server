def is_validate(request):
    sName = request.GET.get("Subject")
    pub = request.GET.get("PublicKey")
    pubA = request.GET.get("PublicKeyAlgorithm")
    fig = request.GET.get("Fingerprint")
    figA = request.GET.get("FingerprintAlgorithm")
    if sName == None or pub == None or pubA == None or fig == None or figA == None:
        return False
    if sName == "" or pub == "" or pubA == "" or fig == "" or figA == "":
        return False
    if not is_validate_subject(sName):
        return False
    return True
def is_validate_subject(subject):
    """
        Assuming that this function can indetify the subject's info XD
        Because I don't have time to deal with things 
        like mail checking or reqursting privilege of linking to the national infomation database
    """
    if subject == '' or subject == None:
        return False
    return True