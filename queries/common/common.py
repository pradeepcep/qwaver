from users.models import Referral


# get a Referral object given a ref_code
def get_referral(ref_code):
    if ref_code is None:
        return None
    try:
        if ref_code.isdigit():
            referral = Referral.objects.get(pk=int(ref_code))
        else:
            referral = Referral.objects.get(ref_code=ref_code)
    except Referral.DoesNotExist:
        referral = None
    return referral
