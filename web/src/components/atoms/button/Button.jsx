import styles from "./Button.module.css"


export const Button = ({
    primary,
    secondary,
    accent,
    dark,
    className,
    children,
    ...props
}) => {
    const baseClasses = 'btn ' + styles.appBtn;


    const colorClass = primary
        ? 'bg-primario text-light'
        : secondary
            ? 'bg-secundario'
            : dark
                ? 'bg-dark text-light'
                : accent
                    ? 'bg-accent text-light'
                    : '';


    const allClasses = [baseClasses, colorClass, className].filter(Boolean).join(' ');

    return (
        <button className={allClasses} {...props}>
            {children}
        </button>
    );
};