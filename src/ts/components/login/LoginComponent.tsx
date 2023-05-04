import React from "react";
import { DashComponentProps } from "../../props";
import './styles.css'
import { borderRadius, color } from "styled-system";
/**
 * Component description
 */
type Props = {
  // Insert props
} & DashComponentProps;

const st = {
  hoverStyleMainBtn: {
    fontFamily: 'Nunito', 
    fontSize: '1.6rem', 
    padding:'1.5rem 6rem', 
    background: '#2B454E', 
    color:'white', border:'none', 
    borderRadius:'4px 0 0 4px',
    cursor: 'pointer',
    '&:hover': { background: '#000' },
  },
  hoverStyleSecondaryBtn:{
    fontFamily: 'Nunito',
    fontSize: '1.6rem', 
    padding:'1.5rem 6rem', 
    background: 'rgb(185 185 185)', 
    color:'black', 
    border:'none', 
    borderRadius:'0px 4px 4px 0',
    cursor: 'pointer'
  }
};

const LoginComponent = (props: Props) => {
  const { id } = props;
  return (
   <div style={{background: 'white', height: '100vh'}}>
    <section style={{
                    display: 'flex', 
                    justifyContent:'space-between', 
                    padding:'4rem'}}
    >
      <p style={{
      fontSize:'2rem', 
      fontWeight: '700', 
      fontFamily: 'Nunito',
      color: '#2B454E'
      }}>
        ABCompany
      </p>
      <section>
        <p style={{
          fontSize:'1.6rem', 
          fontFamily: 'Nunito',
          fontWeight: '500'
        }}
        >
            Novo usuário? 
            <span style={{
              fontSize:'1.6rem', 
              fontFamily: 'Nunito', 
              color: '#2B454E',
              fontWeight: '500'
            }}
            > Entrar
            </span>
       </p>
      </section>
    </section>
    
    <section style={{
      display: 'flex', 
      gap: '10px',
      justifyContent:'center',
      }}>
      <div style={{ 
        backgroundImage: "url('../../../../assets/loginIMG.jpg')", 
        height:'540px', 
        width: '540px',
        backgroundRepeat: 'no-repeat',
        backgroundSize: 'contain',
        }}>
      </div>
      <div>
        <h3 style={{fontFamily: 'Nunito', fontSize: '3.2rem'}}>Welcome Back!</h3>
        <p style={{fontFamily: 'Nunito', fontSize: '1.6rem', color: 'rgb(185 185 185)'}}>Login to continue</p>
        
        <div style={{
          display:'flex', 
          flexDirection:'column', 
          gap:'15px',
          marginTop: '35px'
          }}>
          <span>
            {/* icon */}
            <input type="text" placeholder="Digite o seu nome" style={{fontSize:'1.6rem', padding:'1rem 2rem', width: '41rem', borderRadius: '4px'}} />
          </span>
          <span>
            {/* icon */}
            <input type="password" placeholder="Digite a sua password" name="" id="" style={{fontSize:'1.6rem',  padding:'1rem 2rem', width: '41rem', borderRadius: '4px'}}/>
          </span>
        </div>
        <div style={{marginTop:'25px'}}>
            <a href="/dashboard">
              <button style={st.hoverStyleMainBtn}
                >Login
              </button>
            </a>
            
            <button style={st.hoverStyleSecondaryBtn}>Forget Password?
              </button>
        </div>
        <div style={{marginTop:'25px', cursor:'pointer'}}>
          <span style={{display: 'flex', gap: '5px'}}>
            <p style={{fontFamily: 'Nunito',fontSize:'1.6rem', color: 'rgb(185 185 185)'}}>Login With</p>
            <img src="https://img.icons8.com/color/48/null/google-logo.png" width="5%"/>
          </span>
        </div>
      </div>
    </section>
   </div>
  );
};

export default LoginComponent;
