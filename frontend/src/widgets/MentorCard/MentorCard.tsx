import { IMentor } from "@/src/lib/types";
import Image from "next/image";
import { FC, useState } from "react";
import { useRouter } from "next/navigation";
import styles from "./MentorCard.module.css";
import Loader from "@/src/components/Loader/Loader";

interface MentorCardProps {
  mentor: IMentor;
  percentage: number;
}

const MentorCard: FC<MentorCardProps> = ({ mentor, percentage }) => {
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleMoreClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    setIsLoading(true);
    router.push(`/search/${mentor.mentor_id}`);
  };

  return (
    <div className={styles.card}>
      <div className={styles.compatibility}>
        Совпадение: {Math.round(percentage * 100)}%
      </div>
      <div className={styles.avatarWrapper}>
        <Image
          src="/avatarIcon.png" // замените на реальное изображение, если оно есть
          alt={mentor.name}
          width={100}
          height={100}
          className={styles.avatar}
        />
      </div>
      <div className={styles.header}>
        <h3 className={styles.name}>{mentor.name}</h3>
        {mentor.expertise && (
          <span className={styles.expertise}>{mentor.expertise}</span>
        )}
      </div>
      <div className={styles.rating}>⭐ {mentor.score.toFixed(1)}</div>
      <p className={styles.description}>{mentor.bio}</p>
      <div className={styles.skills}>
        {mentor.tags.map((tag, index) => (
          <span key={index} className={styles.skill}>
            {tag}
          </span>
        ))}
      </div>
      <div className={styles.footer}>
        <span className={styles.requests}>
          {mentor.requests?.length || 0} заявок
        </span>
        <a
          href={`/search/${mentor.mentor_id}`}
          onClick={handleMoreClick}
          className={styles.moreBtn}
        >
          {isLoading ? <Loader /> : "Подробнее"}
        </a>
      </div>
    </div>
  );
};

export default MentorCard;
