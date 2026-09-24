import streamlit as st

from auth.auth import register_user, authenticate_user


def initialize_session() -> None:
    """
    Initialize authentication-related Streamlit session state.
    """

    defaults = {
        "authenticated": False,
        "user_id": None,
        "user_name": None,
        "user_email": None,
        "auth_page": "login",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def login_user(user: dict) -> None:
    """
    Store authenticated user information in session state.
    """

    st.session_state["authenticated"] = True
    st.session_state["user_id"] = user["id"]
    st.session_state["user_name"] = user["name"]
    st.session_state["user_email"] = user["email"]
    st.session_state["auth_page"] = "login"


def logout() -> None:
    """
    Log out the current user.
    """

    st.session_state["authenticated"] = False
    st.session_state["user_id"] = None
    st.session_state["user_name"] = None
    st.session_state["user_email"] = None
    st.session_state["auth_page"] = "login"

    st.rerun()


def show_login_page() -> None:
    """
    Display the login page.
    """

    st.markdown(
        """
        <style>
        .auth-container {
            max-width: 480px;
            margin: 50px auto 0 auto;
            padding: 35px;
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.06);
        }

        .auth-brand {
            text-align: center;
            margin-bottom: 25px;
        }

        .auth-brand h1 {
            color: #2563eb;
            margin-bottom: 5px;
        }

        .auth-brand p {
            color: #6b7280;
            margin-top: 0;
        }

        .auth-footer {
            text-align: center;
            color: #6b7280;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    left, center, right = st.columns([1, 2, 1])

    with center:

        st.markdown(
            """
            <div class="auth-brand">
                <h1>IntelliReport AI</h1>
                <p>AI-Powered Multi-Agent Report Generation</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.subheader("Welcome Back")
        st.write("Sign in to continue to your reports.")

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email",
            key="login_email",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password",
        )

        if st.button(
            "Sign In",
            type="primary",
            use_container_width=True,
        ):
            if not email.strip() or not password:
                st.warning("Please enter your email and password.")
                return

            user = authenticate_user(
                email,
                password
            )

            if user is None:
                st.error("Invalid email or password.")
                return

            login_user(user)

            st.success("Login successful!")
            st.rerun()

        st.markdown(
            '<div class="auth-footer">'
            "Don't have an account?"
            "</div>",
            unsafe_allow_html=True,
        )

        if st.button(
            "Create Account",
            use_container_width=True,
        ):
            st.session_state["auth_page"] = "signup"
            st.rerun()


def show_signup_page() -> None:
    """
    Display the signup page.
    """

    st.markdown(
        """
        <style>
        .auth-brand {
            text-align: center;
            margin-bottom: 25px;
        }

        .auth-brand h1 {
            color: #2563eb;
            margin-bottom: 5px;
        }

        .auth-brand p {
            color: #6b7280;
            margin-top: 0;
        }

        .auth-footer {
            text-align: center;
            color: #6b7280;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    left, center, right = st.columns([1, 2, 1])

    with center:

        st.markdown(
            """
            <div class="auth-brand">
                <h1>IntelliReport AI</h1>
                <p>Create your account</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.subheader("Create Account")

        name = st.text_input(
            "Full Name",
            placeholder="Enter your full name",
            key="signup_name",
        )

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email",
            key="signup_email",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Minimum 8 characters",
            key="signup_password",
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            key="signup_confirm_password",
        )

        if st.button(
            "Create Account",
            type="primary",
            use_container_width=True,
        ):
            if not name.strip():
                st.warning("Please enter your full name.")
                return

            if not email.strip():
                st.warning("Please enter your email address.")
                return

            if not password:
                st.warning("Please enter a password.")
                return

            if password != confirm_password:
                st.error("Passwords do not match.")
                return

            success, message = register_user(
                name=name,
                email=email,
                password=password,
            )

            if success:
                st.success(message)

                st.session_state["auth_page"] = "login"

                # Clear signup fields.
                st.session_state.pop("signup_name", None)
                st.session_state.pop("signup_email", None)
                st.session_state.pop("signup_password", None)
                st.session_state.pop(
                    "signup_confirm_password",
                    None,
                )

                st.rerun()

            else:
                st.error(message)

        st.markdown(
            '<div class="auth-footer">'
            "Already have an account?"
            "</div>",
            unsafe_allow_html=True,
        )

        if st.button(
            "Back to Sign In",
            use_container_width=True,
        ):
            st.session_state["auth_page"] = "login"
            st.rerun()


def show_auth_page() -> None:
    """
    Display the appropriate authentication page.
    """

    initialize_session()

    if st.session_state["auth_page"] == "signup":
        show_signup_page()
    else:
        show_login_page()