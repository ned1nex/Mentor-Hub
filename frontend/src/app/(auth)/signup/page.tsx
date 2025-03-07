"use client";
import Loader from "@/src/components/Loader/Loader";
import Switch from "@/src/components/Switch/Switch";
import { getToken, setToken } from "@/src/lib/jwt";
import { useAppDispatch } from "@/src/store/hooks";
import { setRole } from "@/src/store/reducers/userSlice";
import { mentorApiSlice } from "@/src/store/services/mentorApiSlice";
import { studentApiSlice } from "@/src/store/services/studentApiSlice";
import { userApiSlice } from "@/src/store/services/userApiSlice";
import NavLink from "@/src/widgets/Header/NavLink/NavLink";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import styles from "./page.module.css";

// Интерфейс для типизации ошибки, возвращаемой API
interface ErrorResponse {
    data?: {
        detail?: string[];
    };
}

const Page = () => {
    const [activeItem, setActiveItem] = useState<number>(0);
    const router = useRouter();
    const dispatch = useAppDispatch();

    const [signUpStudent, { isLoading: isLoadingStudent }] = studentApiSlice.useSignupMutation();
    const [signUpMentor, { isLoading: isLoadingMentor }] = mentorApiSlice.useSignupMutation();
    const [skip, setSkip] = useState<boolean>(true);
    userApiSlice.useGetRoleByTokenQuery(getToken() || "", { skip });

    const [name, setName] = useState("");
    const [email, setEmail] = useState<string>("");
    const [expertise, setExpertice] = useState("");
    const [bio, setBio] = useState("");
    const [tags, setTags] = useState<string>("");
    const [telegram, setTelegram] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string>("");

    const submitBtnHandler = async () => {
        setError(""); // очищаем ошибки перед отправкой

        // Проверка обязательных полей
        if (!name || !email || !password) {
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
        if (activeItem === 1) {
            // Для ментора дополнительные поля обязательны
            if (!expertise || !bio || !tags) {
                setError("Пожалуйста, заполните все обязательные поля для ментора.");
                return;
            }
        }
        try {
            if (activeItem === 0) {
                // Формируем payload для студента
                const payload = { email, name, telegram, password };
                console.log(
                    "Отправляемые данные для регистрации студента:",
                    JSON.stringify(payload, null, 2),
                );
                const response = await signUpStudent(payload).unwrap();
                console.log("Успешная регистрация студента:", response);
                dispatch(setRole({ role: "student" }));
                setToken(response.token);
                setSkip(false);
                router.push("/");
            } else {
                // Формируем payload для ментора
                const payload = {
                    email,
                    name,
                    password,
                    telegram,
                    tags: tags.split(" "),
                    expertise,
                    bio,
                };
                console.log(
                    "Отправляемые данные для регистрации ментора:",
                    JSON.stringify(payload, null, 2),
                );
                const response = await signUpMentor(payload).unwrap();
                console.log("Успешная регистрация ментора:", response);
                setSkip(false);
                dispatch(setRole({ role: "mentor" }));
                setToken(response.token);
                router.push("/mentor");
            }
        } catch (err: unknown) {
            console.error("Ошибка при регистрации:", err);
            const errorResponse = err as ErrorResponse;
            setError(
                errorResponse.data?.detail?.[0] ||
                    "Ошибка при регистрации. Возможно, аккаунт с таким email уже зарегистрирован. Попробуйте снова.",
            );
        }
    };

    const isLoading = isLoadingStudent || isLoadingMentor;

    return (
        <div className={styles.page}>
            <NavLink variant="emphasized" href="/">
                вернуться к поиску
            </NavLink>

            <div className={styles.container}>
                <h2 className={styles.title}>Регистрация</h2>
                <p className={styles.subtitle}>Создайте новую учетную запись в MentorHub</p>

                <Switch
                    items={["Студент", "Ментор"]}
                    activeItem={activeItem}
                    setActiveItem={setActiveItem}
                />

                <form onSubmit={(e) => e.preventDefault()} className={styles.form}>
                    <label>Имя и фамилия</label>
                    <input
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        className={styles.input}
                        type="text"
                        placeholder="Иван Иванов"
                    />

                    <label>Email</label>
                    <input
                        className={styles.input}
                        type="email"
                        placeholder="your.email@example.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />

                    {activeItem === 1 && (
                        <>
                            <label>Ваш опыт</label>
                            <textarea
                                value={expertise}
                                onChange={(e) => setExpertice(e.target.value)}
                                className={styles.input}
                                placeholder=""
                            />
                        </>
                    )}

                    {activeItem === 1 && (
                        <>
                            <label>О себе</label>
                            <textarea
                                value={bio}
                                onChange={(e) => setBio(e.target.value)}
                                className={styles.input}
                                placeholder=""
                            />
                        </>
                    )}

                    {activeItem === 1 && (
                        <>
                            <label>Ваши навыки (напишите через пробел)</label>
                            <textarea
                                value={tags}
                                onChange={(e) => setTags(e.target.value)}
                                className={styles.input}
                                placeholder=""
                            />
                        </>
                    )}

                    <label>Telegram</label>
                    <input
                        value={telegram}
                        onChange={(e) => setTelegram(e.target.value)}
                        className={styles.input}
                        type="text"
                        placeholder="@example"
                    />

                    <label>Пароль</label>
                    <input
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="********"
                        className={styles.input}
                        type="password"
                    />

                    <p className={styles.loginText}>
                        Уже есть аккаунт? <Link href="/login">Войти</Link>
                    </p>

                    {error && <p className={styles.errorText}>{error}</p>}

                    <button
                        onClick={submitBtnHandler}
                        type="submit"
                        className={styles.submitButton}
                        disabled={isLoading}>
                        Зарегистрироваться
                    </button>
                </form>

                {isLoading && (
                    <div className={styles.loaderWrapper}>
                        <Loader />
                    </div>
                )}
            </div>
        </div>
    );
};

export default Page;
