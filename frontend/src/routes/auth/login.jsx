import { replace, useLocation, useNavigate } from "react-router";

import { Alert } from "antd";

import { userLogin } from "../../client/auth.js";
import { LoginForm } from "../../components/Auth/LoginForm.jsx";
import { authProvider } from "./authProvider.jsx";


export function Login() {
    const location = useLocation().search;
    return (
        <LoginForm>
            {location.includes("register") &&
                <GetAlert description="Check your email to confirm it!" />
            }
            {location.includes("verify") &&
                <GetAlert message="Mail is confirmed!" type="success" />
            }
            {location.includes("forgotPassword") &&
                <GetAlert description="Check your email to recover password!" />
            }
            {location.includes("resetPassword") &&
                <GetAlert message="Access restored!" type="success" />
            }
        </LoginForm>
    );
}


export async function loginLoader() {
    if (authProvider.isAuth) {
        return replace("/projects");
    }
    return null;
}


export async function loginAction({ request }) {
    const formData = await request.formData();
    const results = await userLogin(formData);

    const next = new URL(request.url)?.searchParams.get("next");
    const errors = {};

    if (results.detail === "LOGIN_BAD_CREDENTIALS") {
        errors.auth = "Invalid email and/or password!"
        return errors;
    } else if (results.detail === "LOGIN_USER_NOT_VERIFIED") {
        errors.verify = "You are not verified! Check email."
        return errors;
    }

    authProvider.setTrue();
    return replace(next ? next : "/projects");
}


/**
 * Shortens the code when you
 * need several similar alerts.
 * @param {string} message
 * @param {string} type
 * @param {string} description 
 * @returns
 */
function GetAlert({
    message = "Almost done!",
    type = "info",
    description
}) {
    const navigate = useNavigate();
    const handleClose = () => navigate("/login", {replace: true});

    return (
        <Alert
            message={message}
            type={type}
            description={description || null}
            showIcon
            closable
            onClose={handleClose}
        />
    );
}