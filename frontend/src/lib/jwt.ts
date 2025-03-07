import Cookies from "js-cookie";

export function getToken() {
    return Cookies.get("token");
}

export function clearToken() {
    Cookies.remove("token");
}

export function setToken(token: string) {
    Cookies.set("token", token, { secure: true });
}
