import streamlit as st


def render_footer():
    """Render the footer section with sticky bottom positioning"""
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            text-align: center;
            padding: 20px 0;
            font-size: 14px;
            z-index: 999;
            box-shadow: 0 -2px 4px rgba(0,0,0,0.1);
        }
        
        .footer a {
            text-decoration: none;
        }
        
        .footer a:hover {
            text-decoration: underline;
        }
        
        .footer-content {
            max-width: 800px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .footer-links {
            margin-bottom: 8px;
        }
        
        .footer-copyright {
            font-size: 12px;
            color: #aaaaaa;
        }
        
        /* Add padding to main content to prevent footer overlap */
        .main .block-container {
            padding-bottom: 100px;
        }
        
        /* Responsive design for mobile */
        @media (max-width: 768px) {
            .footer {
                font-size: 12px;
                padding: 15px 0;
            }
            .footer-content {
                padding: 0 15px;
            }
            .main .block-container {
                padding-bottom: 90px;
            }
        }
        </style>
        
        <div class="footer">
            <div class="footer-content">
                <div class="footer-links">
                    Developed by <a href="https://spencercain.com" target="_blank">Spencer Cain</a> | 
                    Source code on <a href="https://github.com/srmlcn/ixl-grader" target="_blank">GitHub</a>
                </div>
                <div class="footer-copyright">
                    © 2025 Spencer Cain. All rights reserved.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
