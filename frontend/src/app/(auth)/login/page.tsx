import NavLink from "@/src/widgets/Header/NavLink/NavLink";
import LoginForm from "@/src/widgets/LoginForm/LoginForm";
import styles from "./page.module.css";

export default function Login() {
    return (
        <div className={styles.page}>
            <NavLink variant="emphasized" href="/">
                вернуться к поиску
            </NavLink>
            <LoginForm />
        </div>
    );
}
