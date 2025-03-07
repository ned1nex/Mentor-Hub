"use client";
import Button from "@/src/components/Button/Button";
import { useAppSelector } from "@/src/store/hooks";
import { mentorApiSlice } from "@/src/store/services/mentorApiSlice";
import { requestApiSlice } from "@/src/store/services/requestApiSlice";
import DatePickerModal from "@/src/widgets/DatePickerModal/DatePickerModal";
import Image from "next/image";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import styles from "./page.module.css";

const MentorProfile = () => {
    const [isOpen, setIsOpen] = useState(false);
    const router = useRouter();
    const role = useAppSelector((state) => state.user.role);
    const studentId = useAppSelector((state) => state.user.id);
    const [createRequest] = requestApiSlice.useCreateRequestMutation();
    useEffect(() => {
        if (role === "admin") {
            router.replace("dashboard");
        } else if (role === "mentor") {
            router.replace("mentor");
        }
    }, [role, router]);

    const { mentorId } = useParams();
    const { data: mentor } = mentorApiSlice.useGetMentorByIdQuery(`${mentorId}`);
    if (!mentor) {
        return <p className={styles.error}>Ментор не найден</p>;
    }

    return (
        <div className={styles.container}>
            <DatePickerModal
                isOpen={isOpen}
                onClose={() => {
                    setIsOpen(false);
                }}
                onConfirm={async (date: Date) => {
                    await createRequest({
                        student_id: studentId,
                        mentor_id: mentorId?.toString() || "",
                        query: "",
                        status: "PENDING",
                        date: date.toISOString().substring(0, 10),
                    }).unwrap();
                    router.push("/requests");
                }}
            />
            <div className={styles.profile}>
                <div className={styles.header}>
                    <div className={styles.avatarWrapper}>
                        <Image
                            src="/avatarIcon.png"
                            alt={mentor.name}
                            width={120}
                            height={120}
                            className={styles.avatar}
                        />
                    </div>
                    <div className={styles.basicInfo}>
                        <h1 className={styles.name}>{mentor.name}</h1>
                        <div className={styles.rating}>⭐ {mentor.score.toFixed(1)}</div>
                        <div className={styles.requests}>
                            👨‍🎓 {mentor.requests?.length || 0} заявок
                        </div>
                    </div>
                </div>

                <div className={styles.section}>
                    <h2 className={styles.sectionTitle}>Навыки и Экспертиза</h2>
                    <div className={styles.skills}>
                        {mentor.tags.map((tag, index) => (
                            <span key={index} className={styles.skill}>
                                {tag}
                            </span>
                        ))}
                    </div>
                </div>

                <div className={styles.section}>
                    <h2 className={styles.sectionTitle}>О менторе</h2>
                    <p className={styles.bio}>{mentor.bio}</p>
                </div>

                <div className={styles.section}>
                    <h2 className={styles.sectionTitle}>Опыт работы</h2>
                    <p className={styles.experience}>{mentor.expertise || "Опыт не указан"}</p>
                </div>

                <div className={styles.section}>
                    <h2 className={styles.sectionTitle}>Контакты</h2>
                    <Button
                        onClick={() => {
                            if (!role) router.push("/signup");
                            setIsOpen(true);
                        }}
                        className={styles.contactBtn}>
                        Оставить заявку
                    </Button>
                </div>
            </div>
        </div>
    );
};

export default MentorProfile;
