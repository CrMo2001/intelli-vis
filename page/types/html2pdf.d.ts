// html2pdf.d.ts
declare module 'html2pdf.js' {
  interface Html2PdfOptions {
    margin?: number | [number, number, number, number];
    filename?: string;
    image?: {
      type?: string;
      quality?: number;
    };
    enableLinks?: boolean;
    html2canvas?: {
      scale?: number;
      useCORS?: boolean;
      letterRendering?: boolean;
      [key: string]: any;
    };
    jsPDF?: {
      unit?: string;
      format?: string | [number, number];
      orientation?: 'portrait' | 'landscape';
      compress?: boolean;
      [key: string]: any;
    };
    pagebreak?: {
      mode?: 'avoid-all' | 'css' | 'legacy';
      before?: string | string[];
      after?: string | string[];
      avoid?: string | string[];
    };
  }

  interface Html2PdfInstance {
    set(options: Html2PdfOptions): Html2PdfInstance;
    from(element: HTMLElement | string): Html2PdfInstance;
    save(): Promise<void>;
    output(type: string, options?: any): Promise<any>;
    then(callback: Function): Html2PdfInstance;
    catch(callback: Function): Html2PdfInstance;
  }

  function html2pdf(): Html2PdfInstance;
  function html2pdf(element: HTMLElement | string, options?: Html2PdfOptions): Html2PdfInstance;

  export default html2pdf;
}