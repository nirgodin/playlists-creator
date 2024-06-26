import React from "react";
import { useMemo, useEffect, useState } from "react";
import { useDropzone } from "react-dropzone";
import {
  PHOTO,
  PHOTO_DROPZONE_ACCEPT_STYLE,
  PHOTO_DROPZONE_BASE_STYLE,
  PHOTO_DROPZONE_FOCUSED_STYLE,
  PHOTO_DROPZONE_IMAGE_STYLE,
  PHOTO_DROPZONE_REJECT_STYLE,
  PHOTO_DROPZONE_THUMB_CONTAINER_STYLE,
  PHOTO_DROPZONE_THUMB_INNER_STYLE,
  PHOTO_DROPZONE_THUMB_STYLE,
} from "../consts";
import _ from "underscore";
import PropTypes from "prop-types";

function PhotoDropzone(props) {
  const [errorMessage, setErrorMessage] = useState("");
  const [files, setFiles] = useState([]);

  const { getRootProps, getInputProps, isFocused, isDragAccept, isDragReject } =
    useDropzone({
      multiple: false,
      onDrop: handleDrop,
    });

  function isImage(file) {
    const fileTypeComponents = file.type.split("/");
    const fileType = fileTypeComponents[0];

    return fileType === "image";
  }

  function handleDrop(acceptedFiles) {
    const assignedFiles = [];
    const invalidFiles = [];

    acceptedFiles.forEach((file) => {
      if (isImage(file)) {
        Object.assign(file, { preview: URL.createObjectURL(file) });
        assignedFiles.push(file);
        const reader = new FileReader();
        reader.onload = (e) => {
          let newBody = Array.isArray(props.body) ? props.body[0] : props.body;
          newBody[PHOTO] = e.target.result;
          props.setBody([newBody]);      
        };
        reader.readAsDataURL(file); // Read the file as a Data URL (base64)
        console.log("hi");
      } else {
        invalidFiles.push(file);
      }
    });

    if (!_.isEqual(invalidFiles, [])) {
      setErrorMessage("Invalid file type. Files must be of type Image");
      setFiles([]);
    } else {
      setFiles(assignedFiles);
      setErrorMessage("");
    }
  }

  const thumbs = files.map((file) => (
    <div style={PHOTO_DROPZONE_THUMB_STYLE} key={file.name}>
      <div style={PHOTO_DROPZONE_THUMB_INNER_STYLE}>
        <img
          src={file.preview}
          style={PHOTO_DROPZONE_IMAGE_STYLE}
          onLoad={() => {
            URL.revokeObjectURL(file.preview);
          }}
          alt=""
        />
      </div>
    </div>
  ));

  useEffect(() => {
    return () =>
      files.forEach((file) => URL.revokeObjectURL(file.preview));
  }, [files]);

  const style = useMemo(
    () => ({
      ...PHOTO_DROPZONE_BASE_STYLE,
      ...(isFocused ? PHOTO_DROPZONE_FOCUSED_STYLE : {}),
      ...(isDragAccept ? PHOTO_DROPZONE_ACCEPT_STYLE : {}),
      ...(isDragReject ? PHOTO_DROPZONE_REJECT_STYLE : {}),
    }),
    [isFocused, isDragAccept, isDragReject]
  );

  return (
    <div className="photo-dropzone">
      <div {...getRootProps({ style })}>
        <input {...getInputProps()} />
        <p>Drag here or click to select files</p>
      </div>
      <aside
        style={PHOTO_DROPZONE_THUMB_CONTAINER_STYLE}
        className="photo-preview"
      >
        {thumbs}
      </aside>
      <p className="error-message" key={errorMessage}>
        {errorMessage}
      </p>
    </div>
  );
}

PhotoDropzone.propTypes = {
  body: PropTypes.array,
  setBody: PropTypes.func,
  // files: PropTypes.array,
  // setFiles: PropTypes.func,
};

export default PhotoDropzone;
