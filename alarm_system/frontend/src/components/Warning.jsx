export default function Warning(props) {
  // eslint-disable-next-line react/prop-types
  const warningInfo = props.warningInfo;
  // console.log(props);
  return (
    <section className="warning">
      <button className="warning-btn">✖️</button>
      <h1 style={{ color: 'red', fontSize: '100px' }}>⚠️{warningInfo.warningText}</h1>
      <h1>{warningInfo.detail}</h1>
    </section>
  );
}
