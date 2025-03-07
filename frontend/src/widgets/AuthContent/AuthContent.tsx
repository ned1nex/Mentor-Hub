import styles from "./AuthContent.module.css";

const AuthContent = () => {
    return (
        <aside className={styles.aside}>
            <h1 className={styles.title}>
                Next<span className={styles.highlight}>Step</span>
            </h1>
            <p className={styles.subtitle}>
                Найдите своего ментора для обучения и карьерного роста
            </p>
            <div className={styles.steps}>
                <div className={styles.step}>
                    <div className={styles.stepNumber}>1</div>
                    <div className={styles.stepContent}>
                        <p className={styles.stepTitle}>Выберите ментора</p>
                        <p className={styles.stepSubtitle}>
                            Найдите подходящего ментора исходя из ваших потребностей
                        </p>
                    </div>
                </div>
                <div className={styles.step}>
                    <div className={styles.stepNumber}>2</div>
                    <div className={styles.stepContent}>
                        <p className={styles.stepTitle}>Выберите ментора</p>
                        <p className={styles.stepSubtitle}>
                            Найдите подходящего ментора исходя из ваших потребностей
                        </p>
                    </div>
                </div>
                <div className={styles.step}>
                    <div className={styles.stepNumber}>3</div>
                    <div className={styles.stepContent}>
                        <p className={styles.stepTitle}>Выберите ментора</p>
                        <p className={styles.stepSubtitle}>
                            Найдите подходящего ментора исходя из ваших потребностей
                        </p>
                    </div>
                </div>
            </div>
        </aside>
    );
};

export default AuthContent;
