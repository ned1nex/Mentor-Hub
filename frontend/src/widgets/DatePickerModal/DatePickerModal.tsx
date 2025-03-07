import { Dialog, DialogPanel, DialogTitle, Transition, TransitionChild } from "@headlessui/react";
import { clsx } from "clsx";
import React, { Fragment, useState } from "react";
import styles from "./DatePickerModal.module.css";

function getDaysInMonth(month: number, year: number) {
    const date = new Date(year, month, 1);
    const days: Date[] = [];

    while (date.getMonth() === month) {
        days.push(new Date(date));
        date.setDate(date.getDate() + 1);
    }

    return days;
}

const dayNames = ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"];

interface DatePickerModalProps {
    isOpen: boolean;
    onClose: () => void;
    onConfirm: (date: Date) => Promise<void> | void;
}

const DatePickerModal: React.FC<DatePickerModalProps> = ({ isOpen, onClose, onConfirm }) => {
    const now = new Date();
    const [currentMonth, setCurrentMonth] = useState(now.getMonth());
    const [currentYear, setCurrentYear] = useState(now.getFullYear());
    const [selectedDate, setSelectedDate] = useState<Date>(new Date(Date.now()));
    const daysInMonth = getDaysInMonth(currentMonth, currentYear);

    const firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();

    const leadingEmptyDays = Array(firstDayOfMonth).fill(null);

    const handlePrevMonth = () => {
        if (currentMonth === 0) {
            setCurrentMonth(11);
            setCurrentYear((prev) => prev - 1);
        } else {
            setCurrentMonth((prev) => prev - 1);
        }
    };

    const handleNextMonth = () => {
        if (currentMonth === 11) {
            setCurrentMonth(0);
            setCurrentYear((prev) => prev + 1);
        } else {
            setCurrentMonth((prev) => prev + 1);
        }
    };

    const handleDayClick = (day: Date) => {
        setSelectedDate(day);
    };

    const handleConfirm = () => {
        onConfirm(selectedDate);
        onClose();
    };

    return (
        <Transition appear show={isOpen} as={Fragment}>
            <Dialog as="div" className={styles.modalOverlay} onClose={onClose}>
                <div className={styles.modalWrapper}>
                    <TransitionChild
                        as={Fragment}
                        enter="ease-out duration-200"
                        enterFrom="opacity-0 translate-y-4"
                        enterTo="opacity-100 translate-y-0"
                        leave="ease-in duration-150"
                        leaveFrom="opacity-100 translate-y-0"
                        leaveTo="opacity-0 translate-y-4">
                        <DialogPanel className={styles.modalPanel}>
                            <DialogTitle as="h2" className={styles.modalTitle}>
                                Выберите дату
                            </DialogTitle>

                            {}
                            <div className={styles.controls}>
                                <button onClick={handlePrevMonth}>&lt;</button>
                                <span className={styles.monthYear}>
                                    {new Date(currentYear, currentMonth).toLocaleString("default", {
                                        month: "long",
                                        year: "numeric",
                                    })}
                                </span>
                                <button onClick={handleNextMonth}>&gt;</button>
                            </div>

                            {}
                            <div className={styles.calendarGrid}>
                                {dayNames.map((dayName) => (
                                    <div key={dayName} className={styles.dayHeader}>
                                        {dayName}
                                    </div>
                                ))}
                            </div>

                            {}
                            <div className={styles.calendarGrid}>
                                {leadingEmptyDays.map((_, idx) => (
                                    <div key={`empty-${idx}`} />
                                ))}
                                {daysInMonth.map((day) => {
                                    const dayNumber = day.getDate();
                                    const isSelected =
                                        selectedDate &&
                                        day.toDateString() === selectedDate.toDateString();
                                    return (
                                        <div
                                            key={day.toISOString()}
                                            className={
                                                isSelected
                                                    ? clsx(styles.dayCell, styles.dayCellSelected)
                                                    : styles.dayCell
                                            }
                                            onClick={() => handleDayClick(day)}>
                                            {dayNumber}
                                        </div>
                                    );
                                })}
                            </div>

                            <div className={styles.buttonRow}>
                                <button className={styles.closeButton} onClick={onClose}>
                                    Закрыть
                                </button>
                                <button className={styles.confirmButton} onClick={handleConfirm}>
                                    Отправить
                                </button>
                            </div>
                        </DialogPanel>
                    </TransitionChild>
                </div>
            </Dialog>
        </Transition>
    );
};

export default DatePickerModal;
