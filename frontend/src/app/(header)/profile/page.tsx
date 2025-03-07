"use client";
import Subtitle from "@/src/components/Subtitle/Subtitle";
import Textarea from "@/src/components/Textarea/Textarea";
import Title from "@/src/components/Title/Title";
import ProfileInfo from "@/src/widgets/ProfileInfo/ProfileInfo";
import styles from "./page.module.css";
import { useRouter } from "next/navigation";
import { useAppSelector } from "@/src/store/hooks";
import { useEffect, useState } from "react";
import { IMentor, IStudent } from "@/src/lib/types";
import { mentorApiSlice } from "@/src/store/services/mentorApiSlice";
import { studentApiSlice } from "@/src/store/services/studentApiSlice";

function Profile() {
    const router = useRouter();
    const { role, id } = useAppSelector((state) => state.user);
    useEffect(() => {
        if (role === "admin") {
            router.replace("dashboard");
        }
    }, [role, router]);
    const [profile, setProfile] = useState<IMentor | IStudent | null>(null);
    const { data: mentor } = mentorApiSlice.useGetMentorByIdQuery(id);
    const { data: student } = studentApiSlice.useGetStudentQuery(id);
    useEffect(() => {
        console.log(id)
    }, [id])
    useEffect(() => {
        if (role === "student") {
            setProfile(student || null);
        } else {
            setProfile(mentor || null);
        }
    }, [mentor, role, student]);

    return (
        <div className={styles.container}>
            <Title>Профиль</Title>
            <ProfileInfo
                email={profile?.email || ""}
                username={profile?.name || ""}
                tg={profile?.telegram || ""}
                isMentor={role === "mentor"}
                xp={42}
            />
            <Subtitle>О себе</Subtitle>
            <Textarea
                spellCheck={false}
                defaultValue={profile?.bio}
                placeholder="Напишите о себе"
            />
            {profile && "expertise" in profile && (
                <>
                    <Subtitle>Опыт</Subtitle>
                    <Textarea
                        spellCheck={false}
                        defaultValue={profile?.expertise}
                        placeholder="Напишите про свой опыт"
                    />
                </>
            )}
        </div>
    );
}

export default Profile;
