import davidBowieFailureImage from '../static/david_bowie_failure_picture.jpeg';


export default function ErrorPage() {
    return (
        <div className='error-page'>
            {<img src={davidBowieFailureImage} alt="Logo" />}
            <h1>Error!</h1>
        </div>
    )
}