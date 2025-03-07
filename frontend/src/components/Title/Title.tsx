import { HTMLAttributes, ReactNode } from "react";
import styles from "./Title.module.css";

function Title({ children, ...props }: HTMLAttributes<HTMLDivElement> & { children: ReactNode }) {
    return (
        <h1 {...props} className={styles.title}>
            {children}
        </h1>
    );
}

export default Title;
