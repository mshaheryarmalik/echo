"use client";

import { useState, useEffect } from 'react'
import useMasonry from "@/utils/useMasonry";
import Image, { StaticImageData } from "next/image";
import TestimonialImg01 from "@/public/images/testimonial-01.jpg";
import ClientImg01 from "@/public/images/client-logo-01.svg";
import Markdown from 'react-markdown'
import remarkGfm from 'remark-gfm'


interface Testimonials {
  data: any;
}

interface Report {
  reportData: any;
}

const defaultReport = [
  {
    reportData: "As a content creator, I was always on the lookout for a tool that could help me keep up with the demand. The AI-driven content tool has been a game-changer. It generates high-quality content in a fraction of the time it used to take me.",
  }]


export default function Testimonials({reportData}: Report) {
  const masonryContainer = useMasonry();
  const [category, setCategory] = useState<number>(1);
  const [recievedReport, setReport] = useState<String>('');
  const [markdownContent, setMarkdownContent] = useState('');
  const markdown = '## Overview This component allows you to integrate Google Maps into your application with custom markers.'

  useEffect(() => {
    setReport(reportData);
  }, [reportData]);

  // useEffect(() => {
  //   const fetchMarkdown = async () => {
  //     try {
  //       const response = await fetch('junction_frontend/public/temp.md');
  //       const text = await response.text();
  //       setMarkdownContent(text);
  //     } catch (error) {
  //       // console.error('Error loading markdown:', error);
  //     }
  //   };
    
  //   fetchMarkdown();
  // }, []);


  return (
    <div className="mx-auto max-w-6xl px-4 sm:px-6">
      <div className="border-t py-12 [border-image:linear-gradient(to_right,transparent,theme(colors.slate.400/.25),transparent)1] md:py-20">
        {/* Section header */}
        <div className="mx-auto max-w-3xl pb-12 text-center">
          <h2 className="animate-[gradient_6s_linear_infinite] bg-[linear-gradient(to_right,theme(colors.gray.200),theme(colors.indigo.200),theme(colors.gray.50),theme(colors.indigo.300),theme(colors.gray.200))] bg-[length:200%_auto] bg-clip-text pb-4 font-nacelle text-3xl font-semibold text-transparent md:text-4xl">
            Find Your Generated Report Below
          </h2>
          <p className="text-lg text-indigo-200/65">
              Generate insightful, data-driven reports on forest conditions and environmental trends from satellite imagery,
              tailored to specific geographic areas.
          </p>
        </div>

        {/* <div> */}
          {/* Buttons */}
         

          {/* Cards */}
          <div
            className="mx-auto max-w-sm items-start gap-6 sm:max-w-none"
            ref={masonryContainer}
          >
          <Testimonial report={reportData} category={category}>
              {''}
          </Testimonial>
          </div>
        {/* </div> */}
      </div>
    </div>
  );
}

export function Testimonial({
  report,
  category,
  children,
}: {
  report:String;
  category: number;
  children: React.ReactNode;
}) {
  return (
    <article
      className={`relative rounded-2xl bg-gradient-to-br from-gray-900/50 via-gray-800/25 to-gray-900/50 p-5 backdrop-blur-sm transition-opacity before:pointer-events-none before:absolute before:inset-0 before:rounded-[inherit] before:border before:border-transparent before:[background:linear-gradient(to_right,theme(colors.gray.800),theme(colors.gray.700),theme(colors.gray.800))_border-box] before:[mask-composite:exclude_!important] before:[mask:linear-gradient(white_0_0)_padding-box,_linear-gradient(white_0_0)]`}
    >
      <div className="flex flex-col gap-4">
        <div>
          {/* <Image src={report.testimonialsData[0]} height={36} alt="Client logo" /> */}
        </div>
      
        <div className="flex items-center gap-3">
          {/* <Image
            className="inline-flex shrink-0 rounded-full"
            src={report.testimonialsData[0]}
            width={36}
            height={36}
            alt={report.testimonialsData[0]}
          /> */}
          <div className="prose prose-invert max-w-none">
              <Markdown>{report.toString()}</Markdown>
          </div>
        </div>
      </div>
    </article>
  );
}

