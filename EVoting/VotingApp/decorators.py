from django.contrib.auth.decorators import user_passes_test


def mobile_verification_required(f):
    print(lambda u: u.userame)
    return user_passes_test(lambda u: u.mobile_verified, login_url='/verify')(f)


def aadhaar_verification_required(f):
    print(lambda u: u.userame)
    return user_passes_test(lambda u: u.aadhaar_verified, login_url='/verify')(f)
