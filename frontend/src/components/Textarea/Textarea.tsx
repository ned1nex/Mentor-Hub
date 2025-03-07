import { HTMLAttributes } from "react";
import styles from "./Textarea.module.css";

function Textarea({
    placeholder,
    ...props
}: HTMLAttributes<HTMLTextAreaElement> & { placeholder: string }) {
    return <textarea placeholder={placeholder} {...props} className={styles.container} />;
}

export default Textarea;
