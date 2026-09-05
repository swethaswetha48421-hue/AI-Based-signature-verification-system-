import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from src.quality_checker import check_image_quality
from src.verify import verify_signature
from src.database import init_database, save_verification
from src.report_generator import generate_verification_report

class SignatureVerificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Signature Verification System")
        self.root.geometry("700x600")
        
        self.image_path = None
        init_database()
        
        title_label = tk.Label(root, text="SIGNATURE VERIFICATION SYSTEM", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        self.image_frame = tk.Frame(root)
        self.image_frame.pack(pady=10)
        
        self.image_label = tk.Label(self.image_frame, text="No image selected", width=40, height=10, bg="lightgray")
        self.image_label.pack()
        
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        
        upload_btn = tk.Button(btn_frame, text="📁 Upload Signature", command=self.upload_image, width=20)
        upload_btn.grid(row=0, column=0, padx=10)
        
        verify_btn = tk.Button(btn_frame, text="✓ Verify Signature", command=self.verify, width=20, bg="green", fg="white")
        verify_btn.grid(row=0, column=1, padx=10)
        
        self.result_label = tk.Label(root, text="", font=("Arial", 14), fg="blue")
        self.result_label.pack(pady=20)
        
        self.report_btn = tk.Button(root, text="📄 Download Report", command=self.download_report, width=20, state="disabled")
        self.report_btn.pack(pady=5)
        
        self.last_result = None
    
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Signature Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        
        if file_path:
            self.image_path = file_path
            
            img = Image.open(file_path)
            img = img.resize((300, 150), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            
            self.image_label.config(image=img_tk, text="")
            self.image_label.image = img_tk
            
            is_good, message = check_image_quality(file_path)
            
            if not is_good:
                messagebox.showwarning("Quality Warning", f"⚠ {message}\n\nPlease upload a clearer image.")
                self.image_path = None
                self.image_label.config(image="", text="No image selected")
            else:
                messagebox.showinfo("Quality Check", "✅ Image quality is good. You can proceed with verification.")
    
    def verify(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "Please upload a signature image first!")
            return
        
        try:
            result = verify_signature(self.image_path)
            
            self.last_result = {
                'result': result['result'],
                'confidence': result['confidence'],
                'image_path': self.image_path,
                'user_name': 'User'
            }
            
            if result['result'] == 'Genuine':
                self.result_label.config(text=f"✓ Genuine Signature\nConfidence: {result['confidence']:.2f}%", fg="green")
            else:
                self.result_label.config(text=f"⚠ Forged Signature\nConfidence: {result['confidence']:.2f}%", fg="red")
            
            save_verification('User', self.image_path, result['result'], result['confidence'])
            self.report_btn.config(state="normal")
            
        except Exception as e:
            messagebox.showerror("Error", f"Verification failed: {str(e)}")
    
    def download_report(self):
        if self.last_result:
            report_path = generate_verification_report(self.last_result)
            messagebox.showinfo("Report Generated", f"✅ Verification report saved to:\n{report_path}")
        else:
            messagebox.showwarning("Warning", "No verification result to generate report!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SignatureVerificationApp(root)
    root.mainloop()
