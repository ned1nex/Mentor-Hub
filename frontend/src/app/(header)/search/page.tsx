"use client";

import { useAppSelector } from "@/src/store/hooks";
import { IGetMentorsResponse, mentorApiSlice } from "@/src/store/services/mentorApiSlice";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useEffect, useState } from "react";
import SearchFilter from "@/src/features/SearchFilter/SearchFilter";
import MentorCard from "@/src/widgets/MentorCard/MentorCard";
import Loader from "@/src/components/Loader/Loader";
import styles from "./page.module.css";

const Search = () => {
    return (
        <Suspense fallback={<p className={styles.loading}>Загрузка...</p>}>
            <SearchContent />
        </Suspense>
    );
};

const SearchContent = () => {
    const router = useRouter();
    const role = useAppSelector((state) => state.user.role);
    useEffect(() => {
        if (role === "admin") {
            router.replace("dashboard");
        } else if (role === "mentor") {
            router.replace("mentor");
        }
    }, [role, router]);

    const searchParams = useSearchParams();
    const question = searchParams.get("q")?.trim().toLowerCase() || "";
    const { data, isLoading } = mentorApiSlice.useGetMentorsQuery(question);

    const [selectedTags, setSelectedTags] = useState<string[]>([]);
    const [filteredMentors, setFilteredMentors] = useState<IGetMentorsResponse[]>([]);

    const removeTag = (tagToRemove: string) => {
        setSelectedTags((prevTags) => prevTags.filter((tag) => tag !== tagToRemove));
    };

    useEffect(() => {
        if (data) {
            let updatedMentors = data;

            // Фильтрация по выбранным тегам: ментор должен иметь все выбранные теги
            if (selectedTags.length > 0) {
                updatedMentors = updatedMentors.filter((mentor) =>
                    selectedTags.every((tag) => {
                        const tagLower = tag.toLowerCase();
                        const inSkills = mentor.mentor.tags.some(
                            (tag: string) => tag.toLowerCase() === tagLower
                        );
                        const inCategory =
                            mentor.mentor.expertise &&
                            mentor.mentor.expertise.toLowerCase() === tagLower;
                        return inSkills || inCategory;
                    })
                );
            }
            setFilteredMentors(updatedMentors);
        }
    }, [question, selectedTags, data]);

    return (
        <div className={styles.container}>
            <h1 className={styles.title}>Ваш запрос</h1>
            <div className={styles.questionBox}>
                <p>{question || "Нет запроса"}</p>
            </div>
            {/* Вывод выбранных тегов с кнопками для удаления */}
            {selectedTags.length > 0 && (
                <div className={styles.appliedTags}>
                    {selectedTags.map((tag, index) => (
                        <span key={index} className={styles.appliedTag}>
                            {tag}
                            <button
                                onClick={() => removeTag(tag)}
                                className={styles.removeTagButton}
                            >
                                ✖
                            </button>
                        </span>
                    ))}
                </div>
            )}
            <SearchFilter onApplyFilters={setSelectedTags} />
            <div className={styles.cards}>
                {isLoading ? (
                    <div className={styles.loaderWrapper}>
                        <Loader />
                    </div>
                ) : filteredMentors.length > 0 ? (
                    filteredMentors.map((mentor, index) => (
                        <MentorCard
                            percentage={mentor.score}
                            key={index}
                            mentor={mentor.mentor}
                        />
                    ))
                ) : (
                    <p className={styles.noResults}>Менторы не найдены</p>
                )}
            </div>
        </div>
    );
};

export default Search;
