def getRedirect(request):
    """
    Return the "to" parameter from a request, return "/" if no parameter
    """

    value_to = request.GET.get("to", "/")
    value_to = "/" if value_to == "" else value_to

    return value_to