import React from "react";
import "./gallery.css";


const Gallery = ({ data}) => {

  const classes_names = {glioma : "Glioma" , meningioma : "Meningioma", notumor : "No Tumor", pituitary : "Pituitary"}
  return (
    <div className="wrapper">
      <div className="content">
        <div className="row gy-4">
          {data.map((element, index) => (
            <div className="col-lg-3 col-md-6" key={index}>
              <div className="card">
                <div className="card-img">
                  <div className="image-upload">
                  </div>

                  <img
                    src={element.image}
                    alt={element.file_name}
                    class="img-fluid"
                  />
                </div>
                <h3 class="text-center">{element.file_name}</h3>
                {element.result && (
                  <div class="card-body">
                    <div className="body" style={{ marginTop: "-55px" }}>
                      <h3>Results</h3>

                      <section className="line"></section>
                      <div className="line-div">
                        <span className="line-text">Tumor Type :</span>
                        <span className="line-text-result">
                          {classes_names[element.result]}
                        </span>
                      </div>
                      <section className="line"></section>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Gallery;
