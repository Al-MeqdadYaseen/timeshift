from .models import Calculation


def store_calculation_result(request, calc_type, data):
    """Store calculation in session for later saving.

    Also clear any saved flag so the new result can be saved once.
    """
    session_key = f"{calc_type}_result"
    request.session[session_key] = data
    # reset duplicate save prevention
    request.session.pop(f"{calc_type}_saved", None)


def get_stored_result(request, calc_type):
    """Retrieve stored calculation without clearing."""
    session_key = f"{calc_type}_result"
    return request.session.get(session_key)


def clear_stored_result(request, calc_type):
    """Clear stored calculation."""
    session_key = f"{calc_type}_result"
    return request.session.pop(session_key, None)


def save_calculation_to_db(request, calc_type, messages_obj):
    """Generic save handler for both calculation types."""
    result = get_stored_result(request, calc_type)

    if not result:
        messages_obj.error(request, "No calculation to save.")
        return False
    # prevent duplicate saves
    if request.session.get(f"{calc_type}_saved"):
        messages_obj.info(request, "Calculation has already been saved.")
        return False

    try:
        if calc_type == "relativistic":
            Calculation.objects.create(
                calculation_type="relativistic",
                velocity=result["velocity"],
                proper_time=result["proper_time"],
                gamma=result["gamma"],
                dilated_time=result["dilated_time"],
            )
        elif calc_type == "gravitational":
            Calculation.objects.create(
                calculation_type="gravitational",
                proper_time=result["proper_time"],
                dilated_time=result["dilated_time"],
                gravitational_factor=result["gravitational_factor"],
                object_key=result["object_key"],
                object_name=result["object_name"],
            )

        messages_obj.success(request, f"{calc_type.title()} calculation saved!")
        # mark as saved to prevent duplicates
        request.session[f"{calc_type}_saved"] = True
        # Do not clear session after successful save to preserve results
        return True

    except Exception as e:
        messages_obj.error(request, f"Failed to save: {str(e)}")
        return False
