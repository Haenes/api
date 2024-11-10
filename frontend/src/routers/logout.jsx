import { redirect } from "react-router-dom";
import { userLogout} from "../client/auth.js";


export async function logoutAction() {
    const res = await userLogout();
    console.log(res);

    return res.ok ? redirect("/login") : console.log(res);
}
