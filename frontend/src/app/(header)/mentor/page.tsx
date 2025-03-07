"use client";
import { useEffect, useState } from "react";
import styles from "./page.module.css";
import Image from "next/image";
import { useAppSelector } from "@/src/store/hooks";
import { useRouter } from "next/navigation";
import { requestApiSlice } from "@/src/store/services/requestApiSlice";
import { IRequest } from "@/src/lib/types";
import { getToken } from "@/src/lib/jwt";
import { userApiSlice } from "@/src/store/services/userApiSlice";

const MentorDashboard = () => {
    const router = useRouter();
    const role = useAppSelector((state) => state.user.role);
    useEffect(() => {
        if (role === "admin") {
            router.replace("dashboard");
        } else if (role === "student") {
            router.replace("/");
        }
    }, [role, router]);
    userApiSlice.useGetRoleByTokenQuery(getToken() || "");
    const mentorId = useAppSelector((state) => state.user.id);
    const { data: requests } = requestApiSlice.useGetRequestsByMentorIdQuery(mentorId);
    const [editRequest] = requestApiSlice.useEditRequestMutation();
    const [selectedQuestion, setSelectedQuestion] = useState<string | null>(null);

    const getCategoryIcon = (status: IRequest["status"]) => {
        switch (status) {
            case "PENDING":
                return "/awaitingApply.png";
            case "ACCEPTED":
                return "/approvedApply.png";
            case "REFUSED":
                return "/rejectedApply.png";
            default:
                return "";
        }
    };
    const editRequestButtonHandler = (
        status: IRequest["status"],
        request_id: IRequest["request_id"],
    ) => {
        editRequest({ status, request_id });
    };
    const renderRequests = (status: IRequest["status"]) => {
        const filteredRequests: IRequest[] = requests
            ? status === "PENDING"
                ? requests?.filter((el) => el.status === "PENDING")
                : status === "ACCEPTED"
                  ? requests?.filter((el) => el.status === "ACCEPTED")
                  : requests?.filter((el) => el.status === "REFUSED")
            : [];
        return (
            <div className={styles.requestCategory}>
                <div className={styles.categoryHeader}>
                    <h2 className={styles.categoryTitle}>
                        {status === "PENDING"
                            ? "Заявки ожидающие принятия"
                            : status === "ACCEPTED"
                              ? "Принятые заявки"
                              : "Отклонённые заявки"}
                    </h2>
                    <Image src={getCategoryIcon(status)} alt={status} width={100} height={100} />
                </div>
                <div className={styles.requestList}>
                    {filteredRequests.map((req) => (
                        <div key={req.request_id} className={styles.request}>
                            {/* <Image
                                src={req.avatar}
                                alt={req.name}
                                className={styles.avatar}
                                width={70}
                                height={70}
                            /> */}
                            <div className={styles.requestInfo}>
                                <p className={styles.name}>{req.student_id}</p>
                                <p
                                    className={styles.question}
                                    onClick={() => setSelectedQuestion(req.query)}>
                                    {req.query.slice(0, 50)}...
                                </p>
                            </div>
                            {status === "PENDING" && (
                                <div className={styles.actions}>
                                    <button
                                        className={styles.actionBtn}
                                        onClick={() =>
                                            editRequestButtonHandler("PENDING", req.request_id)
                                        }>
                                        <Image
                                            src="/approveTick.png"
                                            alt="Принять"
                                            width={60}
                                            height={60}
                                        />
                                    </button>
                                    <button
                                        className={styles.actionBtn}
                                        onClick={() =>
                                            editRequestButtonHandler("REFUSED", req.request_id)
                                        }>
                                        <Image
                                            src="/rejectApply.png"
                                            alt="Отклонить"
                                            width={60}
                                            height={60}
                                        />
                                    </button>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        );
    };

    return (
        <div className={styles.container}>
            <h1 className={styles.title}>Личный кабинет ментора</h1>
            {renderRequests("PENDING")}
            {renderRequests("ACCEPTED")}
            {renderRequests("REFUSED")}

            {selectedQuestion && (
                <div className={styles.popup} onClick={() => setSelectedQuestion(null)}>
                    <div className={styles.popupContent} onClick={(e) => e.stopPropagation()}>
                        <h2>Полный вопрос</h2>
                        <p>{selectedQuestion}</p>
                        <button
                            onClick={() => setSelectedQuestion(null)}
                            className={styles.closeBtn}>
                            Закрыть
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default MentorDashboard;
