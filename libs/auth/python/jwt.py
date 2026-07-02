def get_requesting_user(event) -> str:
    """
    Get the requesting user from JWT in the Lambda event.
    Args:
        event: Dict containing the Lambda function event data

    Returns:
        User ID of the requesting user from the JWT claims, or an empty string if not found.
    """
    authoriser_details = event.get("requestContext", {}).get("authorizer", {})
    sub = authoriser_details.get("jwt", {}).get("claims", {}).get("sub")
    return "USER#" + sub if sub else ""