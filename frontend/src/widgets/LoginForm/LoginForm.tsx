"use client";
import Loader from "@/src/components/Loader/Loader";
import Switch from "@/src/components/Switch/Switch";
import { setToken } from "@/src/lib/jwt";
import { useAppDispatch } from "@/src/store/hooks";
import { setRole } from "@/src/store/reducers/userSlice";
import { adminApiSlice } from "@/src/store/services/adminApiSlice";
import { mentorApiSlice } from "@/src/store/services/mentorApiSlice";
import { studentApiSlice } from "@/src/store/services/studentApiSlice";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import styles from "./LoginForm.module.css";

// Интерфейс для типизации ошибки, возвращаемой API
interface ErrorResponse {
    data?: {
        detail?: string[];
    };
}

const LoginForm = () => {
    const dispatch = useAppDispatch();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [activeItem, setActiveItem] = useState<number>(0);
    const [error, setError] = useState<string>("");
    const router = useRouter();

    const [loginStudent, { isLoading: isLoadingLoggingInStudent }] =
        studentApiSlice.useLoginMutation();
    const [loginMentor, { isLoading: isLoadingLoggingInMentor }] =
        mentorApiSlice.useLoginMutation();
    const [loginAdmin, { isLoading: isLoadingLoggingInAdmin }] = adminApiSlice.useLoginMutation();

    const handleLogin = async () => {
        setError(""); // очищаем предыдущие ошибки

        // Базовая проверка обязательных полей
        if (!email || !password) {
            setError("Пожалуйста, заполните все обязательные поля.");
            return;
        }
        // Проверка формата email
        const emailRegex = /^\S+@\S+\.\S+$/;
        if (!emailRegex.test(email)) {
            setError("Некорректный формат email.");
            return;
        }
        // Проверка длины пароля
        if (password.length < 8) {
            setError("Пароль должен содержать не менее 8 символов.");
            return;
        }
        try {
            if (activeItem === 0) {
                const response = await loginStudent({ email, password }).unwrap();
                console.log("Студент вошёл:", response);
                dispatch(setRole({ role: "student" }));
                setToken(response.token);
                router.push("/profile");
            } else if (activeItem === 1) {
                const response = await loginMentor({ email, password }).unwrap();
                console.log("Ментор вошёл:", response);
                dispatch(setRole({ role: "mentor" }));
                setToken(response.token);
                router.push("/mentor");
            } else {
                const response = await loginAdmin({ email, password }).unwrap();
                console.log("Админ вошёл:", response);
                dispatch(setRole({ role: "admin" }));
                setToken(response.token);
                router.push("/dashboard");
            }
        } catch (err: unknown) {
            console.error("Ошибка при входе:", err);
            const errorResponse = err as ErrorResponse;
            setError(errorResponse.data?.detail?.[0] || "Ошибка при входе. Попробуйте снова.");
        }
    };

    const isLoading =
        isLoadingLoggingInStudent || isLoadingLoggingInMentor || isLoadingLoggingInAdmin;

    return (
        <div className={styles.wrapper}>
            <div className={styles.titleBlock}></div>
            <p className={styles.title}>Вход в систему</p>
            <p className={styles.subtitle}>Войдите в свою учетную запись MentorHub</p>
            <Switch
                items={["Студент", "Ментор", "Админ"]}
                activeItem={activeItem}
                setActiveItem={setActiveItem}
            />
            <div className={styles.inputBlock}>
                <p className={styles.inputLabel}>Email</p>
                <input
                    placeholder="your.email@example.com"
                    type="text"
                    className={styles.input}
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
            </div>
            <div className={styles.inputBlock}>
                <p className={styles.inputLabel}>Пароль</p>
                <input
                    type="password"
                    className={styles.input}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
            </div>
            <div className={styles.linkBlock}>
                <Link className={styles.link} href={""}>
                    Забыли пароль?
                </Link>
                <Link className={styles.link} href={"/signup"}>
                    Регистрация
                </Link>
            </div>
            {error && <p className={styles.errorText}>{error}</p>}
            <button onClick={handleLogin} className={styles.btn} disabled={isLoading}>
                Войти
            </button>
            {isLoading && (
                <div className={styles.loaderWrapper}>
                    <Loader />
                </div>
            )}
        </div>
    );
};

export default LoginForm;
