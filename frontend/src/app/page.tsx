"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Header from "../widgets/Header/Header";
import styles from "./page.module.css";
import { useAppSelector } from "../store/hooks";
import { userApiSlice } from "../store/services/userApiSlice";
import { getToken } from "../lib/jwt";

const Menu = () => {
    const router = useRouter();
    const role = useAppSelector((state) => state.user.role);

    useEffect(() => {
        if (role === "admin") {
            router.replace("dashboard");
        } else if (role === "mentor") {
            router.replace("mentor");
        }
    }, [role, router]);
    userApiSlice.useGetRoleByTokenQuery(getToken() || "");

    const [question, setQuestion] = useState("");
    const predefinedProblems = [
        "Не могу исправить ошибку компоненте React",
        "Не получается настроить Redux. Проблема может быть в синхронизации с сервером.",
        "Как подключить внешний API? Возникает ошибка CORS.",
    ];

    const handleSearch = () => {
        if (question.trim() !== "") {
            router.push(`/search?q=${encodeURIComponent(question)}`);
        }
    };

    const handlePredefinedClick = (text: string) => {
        setQuestion(text);
    };

    return (
        <div className={styles.wrapper}>
            <Header />
            <div className={styles.container}>
                <h1 className={styles.title}>Описание проблемы</h1>
                <textarea
                    className={styles.textarea}
                    placeholder="Опишите вашу проблему или запрос..."
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                />
                <div className={styles.predefinedContainer}>
                    <div className={styles.predefinedList}>
                        {predefinedProblems.map((problem, index) => (
                            <button
                                key={index}
                                className={styles.predefinedItem}
                                onClick={() => handlePredefinedClick(problem)}>
                                {problem}
                            </button>
                        ))}
                    </div>
                </div>
                <button className={styles.searchBtn} onClick={handleSearch}>
                    Найти ментора
                </button>
            </div>
        </div>
    );
};

export default Menu;
