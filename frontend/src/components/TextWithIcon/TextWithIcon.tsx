import { HTMLAttributes, ReactNode } from "react";
import styles from "./TextWithIcon.module.css";

function TextWithIcon({
    children,
    ...props
}: HTMLAttributes<HTMLDivElement> & { children: ReactNode }) {
    return (
        <h1 {...props} className={styles.container}>
            {children}
        </h1>
    );
}

export default TextWithIcon;
