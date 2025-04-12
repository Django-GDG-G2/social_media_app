Here's the updated version of your documentation, now including the email verification section as requested:

---

# Documentation for Authentication and User Management API

This documentation describes the views, serializers, and endpoints for managing user authentication, registration, profiles, and user actions such as following and unfollowing other users. The API utilizes Django Rest Framework and JWT for token-based authentication.

## Table of Contents

1. [Authentication Views](#authentication-views)
    - User Login (`UserLoginView`)
    - User Logout (`UserLogoutView`)
2. [User Profile Management](#user-profile-management)
    - View User Profiles (`UserProfileView`)
    - Edit User Profile (`UserProfileView`)
3. [User Registration](#user-registration)
    - Register User (`registerUser`)
    - Verify Email (`VerifyEmailView`)
4. [User Follow and Unfollow](#user-follow-and-unfollow)
    - Follow User (`FollowUserView`)
    - Unfollow User (`UnfollowUserView`)
5. [Password Management](#password-management)
    - Forgot Password (`ForgotPasswordAPIView`)
    - Password Reset (`ForgotPasswordAPIView`)
6. [Utilities](#utilities)
    - Token Generation and Validation

---

## Authentication Views

### UserLoginView

This view handles user login via email and password and returns a JWT token for authenticated users.

**Endpoint:** `POST /login/`  
**Request Body:** 
```json
{
  "email": "user@example.com",
  "password": "userpassword"
}
```

**Response:** 
```json
{
  "refresh": "refresh_token",
  "access": "access_token"
}
```

- If the credentials are valid, an access and refresh token are returned.
- If invalid, a `400 Bad Request` response is returned with error details.

### UserLogoutView

This view allows a user to log out by blacklisting their refresh token.

**Endpoint:** `POST /logout/`  
**Request Body:** 
```json
{
  "refresh_token": "refresh_token_here"
}
```

**Response:** 
```json
{
  "message": "Logged out successfully"
}
```

---

## User Profile Management

### UserProfileView

This view provides functionality to view and update a user's profile.

#### GET `/profile/<user_id>/`
- Retrieves the profile information of a specific user by ID.
  
#### PUT `/profile/<user_id>/`
- Updates the logged-in user's profile.
- **Request Body:**
  ```json
  {
    "bio": "Updated bio",
    "username": "updated_username"
  }
  ```

- **Response:** 
  ```json
  {
    "username": "updated_username",
    "bio": "Updated bio",
    "email": "user@example.com"
  }
  ```

---

## User Registration

### Register User (`registerUser`)

This view handles user registration, which includes email verification through a token.

**Endpoint:** `POST /register/`  
**Request Body:**
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "userpassword",
  "bio": "This is a bio."
}
```

**Response:** 
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "bio": "This is a bio."
}
```

Upon successful registration, an email is sent to the user for account activation. The user needs to click the activation link to activate their account.

---

### Verify Email (`VerifyEmailView`)

This view handles the email verification process. Once the user clicks the link in the verification email, their account is activated.

**Endpoint:** `GET /verify-email/<token>/`  
**Request Body:** (No body required, the token is passed as part of the URL)

- The `token` is a one-time use verification token sent to the user's email during registration.

**Response:**
```json
{
  "message": "Email verified successfully, account is now active."
}
```

- If the token is invalid or expired, a `400 Bad Request` response is returned with error details.

---

## User Follow and Unfollow

### Follow User (`FollowUserView`)

This view allows a user to follow another user.

**Endpoint:** `POST /follow/<user_id>/`  
**Request Body:** 
```json
{
  "follower": "user_id_here",
  "following": "user_to_follow_id_here"
}
```

**Response:** 
```json
{
  "message": "You are now following <username>"
}
```

### Unfollow User (`UnfollowUserView`)

This view allows a user to unfollow another user.

**Endpoint:** `POST /unfollow/<user_id>/`  
**Response:** 
```json
{
  "message": "You have unfollowed <username>"
}
```

---

## Password Management

### Forgot Password (`ForgotPasswordAPIView`)

This view handles the request for generating a new random password and sending it to the user's registered email.

**Endpoint:** `POST /forgot-password/`  
**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "New password has been sent to your email."
}
```

---

## Utilities

### Token Generation and Validation

#### MyTokenObtainPairView

This view extends `TokenObtainPairView` to customize the JWT response, adding additional user data.

**Serializer Class:** `MyTokenObtainPairSerializer`

- **JWT Tokens:** The tokens returned are used for authentication in protected endpoints across the API.

---

### Dependencies

- `djangorestframework`
- `djangorestframework_simplejwt`

---

