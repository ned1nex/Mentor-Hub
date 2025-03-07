import React from "react";

import styles from "./ProgressBar.module.css";

type ProgressBarProps = {
    value: number;
    max?: number;
    color?: string;
};

const ProgressBar: React.FC<ProgressBarProps> = ({ value, max = 100 }) => {
    const percentage = (Math.min(Math.max(value, 0), max) / max) * 100;

    return (
        <div className={styles.progressContainer}>
            <div className={styles.progressBar} style={{ width: `${percentage}%` }}></div>
        </div>
    );
};

export default ProgressBar;
