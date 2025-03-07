"use client";
import { clsx } from "clsx";
import styles from "./Avatar.module.css";

function Avatar({ abbreviation, size = 40 }: { abbreviation: string; size?: number }) {
    return (
        <div className={clsx(styles.avatar, styles.fallback)} style={{ width: size, height: size }}>
            <span className={styles.fallbackText} style={{ fontSize: size / 2.5 }}>
                {abbreviation}
            </span>
        </div>
    );
}

export default Avatar;
