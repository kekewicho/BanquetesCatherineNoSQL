export const Image = ({ ...props }) => (
    <img src={props.src} {...props} style={{ objectFit:'contain', ...props.style }} />
)