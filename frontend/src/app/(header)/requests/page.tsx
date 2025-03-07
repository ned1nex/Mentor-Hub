"use client";
import Image from "next/image";
import Link from "next/link";
import { useEffect, useState } from "react";
import styles from "./page.module.css";
import { requestApiSlice } from "@/src/store/services/requestApiSlice";
import { useAppSelector } from "@/src/store/hooks";
import { IRequest } from "@/src/lib/types";

const CollapsibleText = ({ text, threshold = 100 }: { text: string; threshold?: number }) => {
    const [expanded, setExpanded] = useState(false);

    if (text.length <= threshold) {
        return <p className={styles.applicationQuestion}>{text}</p>;
    }

    const displayText = expanded ? text : text.slice(0, threshold) + "...";
    return (
        <div className={styles.applicationQuestion}>
            <p>{displayText}</p>
            <button onClick={() => setExpanded(!expanded)} className={styles.expandBtn}>
                {expanded ? "Свернуть" : "Показать полностью"}
            </button>
        </div>
    );
};

const RequestsPage = () => {
    const studentId = useAppSelector((state) => state.user.id);
    const [pendingRequests, setPendingRequests] = useState<IRequest[]>([]);
    const [acceptedRequests, setAcceptedRequests] = useState<IRequest[]>([]);

    const { data: requests } = requestApiSlice.useGetRequestsByStudentIdQuery(studentId);

    useEffect(() => {
        setPendingRequests(requests?.filter((el) => el.status === "PENDING") || []);
        setAcceptedRequests(requests?.filter((el) => el.status === "ACCEPTED") || []);
    }, [requests]);
    return (
        <div className={styles.wrapper}>
            <div className={styles.container}>
                <div className={styles.applicationsContainer}>
                    <div className={styles.applicationsColumn}>
                        <h2 className={styles.sectionTitle}>Мои принятые заявки</h2>
                        {acceptedRequests.map((app) => (
                            <div key={app.request_id} className={styles.applicationItem}>
                                <div className={styles.applicationDetails}>
                                    <span className={styles.applicationTime}>
                                        Время открытия: {app.date}
                                    </span>
                                    <CollapsibleText text={app.query} threshold={100} />
                                    <Link
                                        href={`/search/${app.mentor_id}`}
                                        className={styles.mentorLink}>
                                        <div className={styles.mentorDetails}>
                                            {/* <Image
                                                src={app.mentorAvatar}
                                                alt={app.mentorName}
                                                width={30}
                                                height={30}
                                                className={styles.mentorAvatar}
                                            /> */}
                                            <span className={styles.mentorName}>
                                                {/* {app.mentorName} */}
                                            </span>
                                        </div>
                                    </Link>
                                </div>
                                <div className={styles.applicationIcon}>
                                    <Image
                                        src="/approvedApply.png"
                                        alt="Принятая заявка"
                                        className={styles.icon}
                                        width={80}
                                        height={80}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                    <div className={styles.applicationsColumn}>
                        <h2 className={styles.sectionTitle}>Ожидающие заявки</h2>
                        {pendingRequests.map((app) => (
                            <div key={app.request_id} className={styles.applicationItem}>
                                <div className={styles.applicationDetails}>
                                    <span className={styles.applicationTime}>
                                        Время открытия: {app.date}
                                    </span>
                                    <CollapsibleText text={app.query} threshold={100} />
                                    <Link
                                        href={`/search/${app.mentor_id}`}
                                        className={styles.mentorLink}>
                                        <div className={styles.mentorDetails}>
                                            {/* <Image
                                                src={app.mentorAvatar}
                                                alt={app.mentorName}
                                                width={30}
                                                height={30}
                                                className={styles.mentorAvatar}
                                            />
                                            <span className={styles.mentorName}>
                                                {app.mentorName}
                                            </span> */}
                                        </div>
                                    </Link>
                                </div>
                                <div className={styles.applicationIcon}>
                                    <Image
                                        src="/awaitingApply.png"
                                        alt="Ожидающая заявка"
                                        className={styles.icon}
                                        width={80}
                                        height={80}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RequestsPage;
