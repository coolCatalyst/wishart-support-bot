import { useState } from "react";
import { postLead } from "./API";
import { LeadCloseIcon } from "./Icons";
import { getCountryCode } from "./API";
export const LeadComponent = ({
  leads_title,
  leads_field=[],
  setClose,
  force,
  chat_id,
  thread_id,
  messageAction,
  datas,
}) => {
  const [values, setValues] = useState({ name: "", email: "", phone: "" });
  const onClose = () => {
    console.log("close");
    setClose(true);
  };
  const handleSubmit = async (event) => {
    event.preventDefault();
    let country_code = await getCountryCode();
    let lead_datas=[{'country':country_code}]
    for(let lead of leads_field){
      lead_datas.push({[lead]: values[lead]});
    }
    console.log(lead_datas);
    const response = await postLead(chat_id, lead_datas);
    if (response == true) {
      setClose(true);
      if (force=="on") {
        messageAction(datas[datas.length-1].message);
      }
    }
  };
  const handleChange = (event) => {
    setValues({
      ...values,
      [event.target.name]: event.target.value,
    });
  };
  return (
    <div className="sai-msg sai-form">
      {force == "off" ? (
        <button type="button" className="close-lead-form" onClick={onClose}>
          <LeadCloseIcon />
        </button>
      ) : (
        <></>
      )}
      <span className="msg-content">{leads_title}</span>
      <form
        action=""
        method="post"
        className="lead-form"
        onSubmit={handleSubmit}
      >
        {leads_field.includes("email") ? (
          <div className="lead-field">
            <label htmlFor="lead-email">Email</label>
            <input
              type="email"
              name="email"
              placeholder="john@email.com"
              value={values.email}
              onChange={handleChange}
            />
          </div>
        ) : (
          <></>
        )}
        {leads_field.includes("name") ? (
          <div className="lead-field">
            <label htmlFor="lead-name">Name</label>
            <input
              type="text"
              name="name"
              placeholder="John Doe"
              value={values.name}
              onChange={handleChange}
            />
          </div>
        ) : (
          <></>
        )}
        {leads_field.includes("phone") ? (
          <div className="lead-field">
            <label htmlFor="lead-phone">Phone</label>
            <input
              type="number"
              name="phone"
              placeholder="(123) 123-1234"
              value={values.phone}
              onChange={handleChange}
            />
          </div>
        ) : (
          <></>
        )}
        <button type="submit" className="submit-button">
          Submit
        </button>
      </form>
    </div>
  );
};
