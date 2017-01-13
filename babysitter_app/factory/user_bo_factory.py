from babysitter_app.model.address import Address
from babysitter_app.model.role import Role
from babysitter_app.model.user import User
from babysitter_app.model.user_role import UserRole

class UserBOFactory():

  @staticmethod
  def create_user_bo(user_type, user_info, user_addr_info):
    """Create a User Business Object

    Arguments:
    user_type -- string
    user_info -- dict, user information
    user_addr_info -- dict, user's address information

    Returns:
    user -- object, user object
    """
    user = User.create_user(user_info)
    address_id = Address.create_address(user.id, user_addr_info)

    if user_type == Role.BABYSITTER_ROLE:
      babysitter_role_id = Role.get_babysitter_role_id()
      UserRole.create_user_role(user.id, babysitter_role_id)

    return user
