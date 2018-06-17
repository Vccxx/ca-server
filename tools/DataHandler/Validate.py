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
    return True