import styles from "./logo.module.css";

function Logo() {
    return (
        <div className={styles.logo}>
            Mentor<span className={styles.logoAccent}>Hub</span>
        </div>
    );
}

export default Logo;
