import { HTMLAttributes, ReactNode } from "react";
import styles from "./Subtitle.module.css";

function Subtitle({
    children,
    ...props
}: HTMLAttributes<HTMLDivElement> & { children: ReactNode }) {
    return (
        <h2 {...props} className={styles.subtitle}>
            {children}
        </h2>
    );
}

export default Subtitle;
