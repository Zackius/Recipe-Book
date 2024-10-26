from rest_framework import response, status


def _check_if_valid_phone_number(phone_number):
    """This function checks if the phone number is valid"""
    try:
        phone_number = str(phone_number)
        if phone_number.startswith("+"):
            if len(phone_number) != 13:
                return response.Response(
                    {"msg": "Invalid phone number"}, status=status.HTTP_400_BAD_REQUEST
                )

            phone_number = phone_number[1:]
        elif phone_number.startswith("254"):
            if len(phone_number) != 12:
                return response.Response(
                    {"msg": "Invalid phone number"}, status=status.HTTP_400_BAD_REQUEST
                )

        elif phone_number.startswith("07"):
            if len(phone_number) != 10:
                return response.Response(
                    {"msg": "Invalid phone number"}, status=status.HTTP_400_BAD_REQUEST
                )
            ## sort the phone number
            phone_number = "254" + phone_number[1:]
        elif phone_number.startswith("01"):
            if len(phone_number) != 10:
                return response.Response(
                    {"msg": "Invalid phone number"}, status=status.HTTP_400_BAD_REQUEST
                )
            ## sort the phone number
            phone_number = "254" + phone_number[1:]

        else:
            return response.Response(
                {"msg": "Invalid phone number"}, status=status.HTTP_400_BAD_REQUEST
            )

        return phone_number

    except Exception as err:
        print(f"An error occurred: {err}")
        return {"error": str(err)}
